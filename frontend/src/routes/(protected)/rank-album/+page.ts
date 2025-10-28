import type { PageLoad } from '../../$types';
import { Track } from '../../types'

export const load: PageLoad = async ({ fetch }) => {
    async function getTracks(): Promise<Track[] | string> {
        try {
            const response = await fetch('http://127.0.0.1:8000/tracks/');
            const json = await response.json();
            return response.ok ? (json as Track[]) : (json.detail as string);
        } catch {
            return "Что-то пошло не так.";
        }
    }
    return {
        tracks: getTracks(),
    };
};

