<script lang="ts">
	import { defaults, superForm } from 'sveltekit-superforms';
	import * as Form from '$lib/components/ui/form/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { zod4, zod4Client } from 'sveltekit-superforms/adapters';
	import { submitSchema, Album } from '../../types';
	import { toast } from 'svelte-sonner';

	const form = superForm(defaults(zod4(submitSchema)), {
		validators: zod4Client(submitSchema),
		onResult({ result }) {
			if (result.type == 'success') {
				const success: boolean = result.data?.success;
				const server: boolean = result.data?.server;
				const message = result.data?.message;
				console.log(message);
				if (server) {
					if (success) {
						const album = message as Album;
						toast.message('Успешно!', {
							description:
								'Альбом ' +
								album.artist +
								' - ' +
								album.name +
								' добавлен на сервер.'
						});
					} else {
						toast.error(message);
					}
				} else {
					toast.error('Что-то пошло не так.');
				}
			}
		}
	});
	const { form: formData, enhance } = form;

	const sources = [
		{
			value: 'discogs',
			label: 'Discogs (master)',
			placeholder: 'https://www.discogs.com/master/2129-Boards-Of-Canada-Geogaddi'
		},
		{
			value: 'spotify',
			label: 'Spotify',
			placeholder: 'https://open.spotify.com/album/6NtqlXVVPSnSUo9Ebg6QQR'
		}
	];
</script>

<div class="flex flex-col items-center space-y-4 p-2">
	<form
		method="POST"
		action="?/albums"
		use:enhance
		class="flex w-full max-w-4xl flex-col space-y-4"
	>
		<Form.Field {form} name="source">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Откуда брать</Form.Label>
					<Select.Root {...props} type="single" bind:value={$formData.source}>
						<Select.Trigger class="w-full"
							>{sources.find((source) => source.value === $formData.source)
								?.label}</Select.Trigger
						>
						<Select.Content>
							{#each sources as source (source.value)}
								<Select.Item value={source.value} label={source.label}
									>{source.label}</Select.Item
								>
							{/each}
						</Select.Content>
					</Select.Root>
				{/snippet}
			</Form.Control>
			<Form.FieldErrors />
		</Form.Field>
		<Form.Field {form} name="link">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Ссылка на альбом</Form.Label>
					<Input
						{...props}
						bind:value={$formData.link}
						placeholder={sources.find((source) => source.value === $formData.source)
							?.placeholder}
					/>
				{/snippet}
			</Form.Control>
			<Form.FieldErrors />
		</Form.Field>
		<Form.Field {form} name="username">
			<Form.Control>
				{#snippet children({ props })}
					<Form.Label>Никнейм</Form.Label>
					<Input {...props} bind:value={$formData.username} />
				{/snippet}
			</Form.Control>
			<Form.FieldErrors />
		</Form.Field>
		<Form.Button class="h-14" variant="outline">Добавить в круг</Form.Button>
	</form>
</div>
