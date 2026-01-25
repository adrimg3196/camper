import { NextResponse } from 'next/server';
import { generateMarketingContent } from '@/lib/gemini';
import { generateVideo } from '@/lib/video';
import path from 'path';
import fs from 'fs';

export async function POST(request: Request) {
    const body = await request.json();
    const { topic, productUrl, platform } = body;

    try {
        // Try to use real Gemini API
        let data;
        if (process.env.GOOGLE_API_KEY) {
            data = await generateMarketingContent(topic, productUrl);
        } else {
            // Fallback to mock if no key provided (for demo/testing)
            console.warn("GOOGLE_API_KEY not found, using mock data");
            await new Promise(resolve => setTimeout(resolve, 1500));
            data = {
                telegram: {
                    content: `🔥 **CHOLLO (MOCK): ${topic}** 🔥\n\n⬇️ Bajada de precio histórica\n✅ Calidad premium\n📦 Envío GRATIS\n\n👉 ${productUrl}\n\n#camping #ofertas`
                },
                tiktok: {
                    script: `(0:00) 😲 MOCK SCRIPT for ${topic}...\n(0:10) Check this out!\n(0:30) Link in bio!`,
                    visualSettings: "Dynamic mock visuals"
                },
                instagram: {
                    caption: `✨ MOCK CAPTION for ${topic}.\n\nLink in bio! #mock #camping`,
                    imagePrompt: "Mock image prompt"
                }
            };
        }

        // Trigger video gen for TikTok
        if (platform === 'tiktok' || !platform) {
            const videoName = `gen_${Date.now()}.mp4`;
            // Use Node's OS temp dir or /tmp for Vercel compatibility
            const tempDir = process.env.VERCEL ? '/tmp' : path.join(process.cwd(), 'public', 'temp');
            const videoPath = path.join(tempDir, videoName);

            // Ensure temp dir exists if local
            if (!process.env.VERCEL && !fs.existsSync(tempDir)) {
                fs.mkdirSync(tempDir, { recursive: true });
            }

            try {
                console.log("Generating video at:", videoPath);
                await generateVideo('public/images/sample.jpg', topic || "Camping Deal", videoPath);

                // Upload to Supabase and clean up
                console.log("Uploading to Supabase...");
                try {
                    const { uploadVideo } = await import('@/lib/supabase');
                    const publicUrl = await uploadVideo(videoPath, videoName);
                    data.tiktok.videoUrl = publicUrl;
                    console.log("Upload success:", publicUrl);

                    // CLEANUP: Delete local file immediately
                    fs.unlinkSync(videoPath);
                    console.log("Local temp file deleted.");
                } catch (uploadError) {
                    console.error("Supabase upload failed, serving local fallback if dev:", uploadError);
                    // If upload fails in local dev, we might keep the file, but user strict rule says delete.
                    // We will try to delete anyway if it was created.
                    if (fs.existsSync(videoPath)) {
                        // In dev we might want to see it, but user said "no local". 
                        // We'll leave it in temp for debugging if upload failed, or delete it?
                        // User said "no quiero nada en local". Deleting.
                        fs.unlinkSync(videoPath);
                    }
                    data.tiktok.videoError = "Upload to cloud failed";
                }

            } catch (videoError) {
                console.error("Video generation failed:", videoError);
                data.tiktok.videoError = "FFmpeg processing failed";
            }
        }

        return NextResponse.json(data);

    } catch (error) {
        console.error("API Error:", error);
        return NextResponse.json(
            { error: "Failed to generate content. Ensure GOOGLE_API_KEY is set." },
            { status: 500 }
        );
    }
}
