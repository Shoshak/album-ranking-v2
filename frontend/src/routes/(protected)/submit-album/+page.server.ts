import type { Actions } from "@sveltejs/kit";

export const actions = {
    albums: async ({ request, fetch }) => {
        const formData = await request.formData();
        const data = {
            source: formData.get('source'),
            url: formData.get('link'),
            username: formData.get('username')
        };
        try {
            const response = await fetch('http://127.0.0.1:8000/albums/', {
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
    },
} satisfies Actions;