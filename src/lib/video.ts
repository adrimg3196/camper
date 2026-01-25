import ffmpeg from 'fluent-ffmpeg';
import path from 'path';
import fs from 'fs';

export async function generateVideo(imagePath: string, text: string, outputPath: string): Promise<string> {
    return new Promise((resolve, reject) => {
        // Ensure output directory exists
        const dir = path.dirname(outputPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }

        // In a real scenario, we would use a library to draw text on the image canvas first 
        // or use complex ffmpeg filters. For this demo, we assume the image is ready-to-use
        // or we just make a static video from the image.

        ffmpeg(imagePath)
            .loop(5) // 5 seconds duration
            .fps(30)
            .videoFilters([
                {
                    filter: 'scale',
                    options: '1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2'
                },
                {
                    filter: 'drawtext',
                    options: {
                        text: text.substring(0, 50), // Limit text length
                        fontsize: 64,
                        fontcolor: 'white',
                        x: '(w-text_w)/2',
                        y: '(h-text_h)/2',
                        shadowcolor: 'black',
                        shadowx: 2,
                        shadowy: 2
                    }
                }
            ])
            .on('end', () => {
                console.log('Video created:', outputPath);
                resolve(outputPath);
            })
            .on('error', (err) => {
                console.error('Error creating video:', err);
                reject(err);
            })
            .save(outputPath);
    });
}
