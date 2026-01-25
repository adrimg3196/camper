import { GoogleGenerativeAI } from "@google/generative-ai";

const apiKey = process.env.GOOGLE_API_KEY;

export async function generateMarketingContent(topic: string, productUrl: string) {
    if (!apiKey) {
        throw new Error("GOOGLE_API_KEY is not defined");
    }

    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-pro" });

    const prompt = `
    You are an expert social media marketer. Generate a JSON object with marketing content for the following product/topic: "${topic}".
    Product URL: ${productUrl}

    The JSON must have this exact structure:
    {
      "telegram": {
        "content": "Short, punchy copy with emojis, price anchor (fake if not provided), and affiliate link."
      },
      "tiktok": {
        "script": "TIMECODED script (0:00, 0:05, etc) with hooks, benefits, and CTA.",
        "visualSettings": "Brief description of visual style"
      },
      "instagram": {
        "caption": "Engaging caption with hashtags",
        "imagePrompt": "Detailed prompt for an image generator (like Midjourney)"
      }
    }
    
    Return ONLY valid JSON.
  `;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    // Clean markdown if present
    const jsonString = text.replace(/```json/g, '').replace(/```/g, '').trim();

    try {
        return JSON.parse(jsonString);
    } catch (e) {
        console.error("Failed to parse Gemini response:", text);
        throw new Error("Invalid JSON from Gemini");
    }
}
