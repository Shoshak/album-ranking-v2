// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		interface Locals {
            user: {
                id: number = 0;
                username: string;
                admin_rights: boolean;
            }
        }
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
