
import { createClient, SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

// Create a mock client for build time when env vars are not available
function createSupabaseClient(): SupabaseClient {
    if (!supabaseUrl || !supabaseKey) {
        // Return a placeholder during build - actual calls will fail gracefully
        console.warn('Supabase credentials not configured');
        return createClient('https://placeholder.supabase.co', 'placeholder-key');
    }
    return createClient(supabaseUrl, supabaseKey);
}

export const supabase = createSupabaseClient();

// Check if Supabase is properly configured
export function isSupabaseConfigured(): boolean {
    return !!supabaseUrl && !!supabaseKey && supabaseUrl !== 'https://placeholder.supabase.co';
}

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
