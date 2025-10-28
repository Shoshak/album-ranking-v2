import type { Actions } from '../../$types';

export const actions = {
    ranking: async ({ request, fetch, url }) => {
        const formData = await request.formData();
        const placements = formData.get('placements') as string
        const album_id = url.searchParams.get('track_id')
        const track_id = url.searchParams.get('track_id')
        const data = {
            username: formData.get('username'),
            placements: placements.split(',').map(placement => parseInt(placement))
        }

        async function getRanking(track_id: string | null) {
            try {
                const response = await fetch('http://127.0.0.1:8000/tracks/' + track_id + "?username=" + data.username);
                return { server: true, success: response.ok }
            }
            catch {
                return {
                    server: false,
                    success: false
                }
            }
        }

        async function patchRanking(album_id: string | null) {
            try {
                const response = await fetch('http://127.0.0.1:8000/albums/' + album_id, {
                    method: 'PATCH',
                    headers: {
                        accept: 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                const json = await response.json()
                return {
                    server: true,
                    success: response.ok as boolean,
                    message: (response.ok ? json : (json.detail as string)) as string
                }
            }
            catch {
                return {
                    server: false,
                    success: false
                }
            }
        }
        const fetchData = async (album_id: string | null) => {
            try {
                const response = await fetch('http://127.0.0.1:8000/albums/' + album_id, {
                    method: 'POST',
                    headers: {
                        accept: 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                const json = await response.json();
                return {
                    server: true,
                    success: response.ok as boolean,
                    message: (response.ok ? json : (json.detail as string)) as string
                }
            }
            catch {
                return {
                    server: false,
                    success: false
                }
            }
        }

        const previousRanking = await getRanking(track_id)
        if (previousRanking.server) {
            if (previousRanking.success) {
                return patchRanking(album_id)
            }
            else {
                return fetchData(album_id)
            }
        }
        else {
            return {
                server: false,
                success: false
            }
        }

    },
} satisfies Actions;