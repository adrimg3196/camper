
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseKey);

export async function uploadVideo(filePath: string, fileName: string) {
    const fileBuffer = require('fs').readFileSync(filePath);

    const { data, error } = await supabase
        .storage
        .from('videos') // Requires a bucket named 'videos' to be public
        .upload(fileName, fileBuffer, {
            contentType: 'video/mp4',
            upsert: true
        });

    if (error) {
        throw error;
    }

    const { data: publicData } = supabase
        .storage
        .from('videos')
        .getPublicUrl(fileName);

    return publicData.publicUrl;
}
