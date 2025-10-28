<script lang="ts">
	import { goto } from '$app/navigation';
	import { toast } from 'svelte-sonner';
	import { Login } from 'sveltegram';

	const signIn = async (data: {
		id: number;
		first_name: string;
		username: string;
		photo_url: string;
		auth_date: number;
		hash: string;
	}) => {
		try {
			const response = await fetch('http://127.0.0.1:8000/sessions/', {
				method: 'POST',
				headers: {
					accept: 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(data)
			});
			const json = await response.json();
			if (response.ok) {
				document.cookie = `session_id=${json.id}`;
				throw goto('/rank-album');
			} else {
				if (response.status == 500) {
					try {
						const response = await fetch(
							'http://127.0.0.1:8000/sessions/?telegram_id=' + data.id
						);
						const json = await response.json();
						document.cookie = `session_id=${json.id}`;
						if (new Date() < new Date(json.expires_at)) {
							throw goto('/rank-album');
						} else {
							data.id = json.id;
							try {
								const response = await fetch('http://127.0.0.1:8000/sessions/', {
									method: 'PATCH',
									headers: {
										accept: 'application/json',
										'Content-Type': 'application/json'
									},
									body: JSON.stringify(data)
								});
								throw goto('/rank-album');
							} catch {
								toast.error('Что-то пошло не так.');
							}
						}
					} catch {}
				} else {
					toast.error(json.detail as string);
				}
			}
		} catch {
			toast.error('Что-то пошло не так.');
		}
	};
</script>

<div class="flex min-h-screen items-center px-4 py-12 sm:px-6 md:px-8 lg:px-12 xl:px-16">
	<div class="w-full space-y-6 text-center">
		<div class="space-y-3">
			<h1 class="text-4xl font-black tracking-tighter sm:text-5xl">album ranking.</h1>
			<Login
				username="RankingAuthBot"
				requestAccess={true}
				onauth={async (data) => {
					signIn(data);
				}}
			/>
		</div>
	</div>
</div>
