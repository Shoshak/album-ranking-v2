import type { PageLoad } from "../../$types"

export const load: PageLoad = async ({ }) => {
    async function getAlbums(): Promise<string[] | string> {
        try {
            const response = await fetch('http://127.0.0.1:8000/albums/');
            const json = await response.json();
            return response.ok ? (json as string[]) : (json.detail as string);
        } catch (error) {
            return "Что-то пошло не так.";
        }
    }
    return {
        albums: getAlbums()
    }
}