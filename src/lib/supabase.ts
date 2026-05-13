import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL as string;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string;

if (!supabaseUrl || !supabaseAnonKey) {
    console.error(
        '[Supabase] VITE_SUPABASE_URL veya VITE_SUPABASE_ANON_KEY eksik.\n' +
        '.env.local dosyasına bu değerleri Supabase Dashboard > Settings > API bölümünden ekleyin.'
    );
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
