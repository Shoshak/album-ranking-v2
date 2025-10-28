<script lang="ts">
	import type { PageProps } from './$types';
	import { defaults, superForm } from 'sveltekit-superforms';
	import * as Form from '$lib/components/ui/form/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Skeleton } from '$lib/components/ui/skeleton/index.js';
	import SortableList from '../../components/SortableList.svelte';
	import { toast } from 'svelte-sonner';
	import { zod4, zod4Client } from 'sveltekit-superforms/adapters';
	import { rankingSchema } from '../../types';

	let { data }: PageProps = $props();

	const form = superForm(defaults(zod4(rankingSchema)), {
		validators: zod4Client(rankingSchema),
		onResult({ result }) {
			if (result.type == 'success') {
				const success: boolean = result.data?.success;
				const message: string = result.data?.message;
				const server: boolean = result.data?.server;
				if (server) {
					if (success) {
						toast.message('Альбом успешно отправлен!');
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
</script>

<div class="flex h-[800px] flex-col items-center space-y-4 p-2">
	{#await data.tracks}
		<Skeleton class="bg-background dark:bg-input/30 h-full w-full max-w-4xl rounded-lg " />
	{:then tracks}
		{#if !(typeof tracks === 'string')}
			<form
				method="POST"
				action={'?/ranking' +
					'&' +
					'album_id=' +
					String(tracks[0].album_id) +
					'&' +
					'track_id=' +
					String(tracks[0].id)}
				use:enhance
				class="flex w-full max-w-4xl flex-col"
			>
				<Form.Field {form} name="username">
					<Form.Control>
						{#snippet children({ props })}
							<Form.Label>Никнейм</Form.Label>
							<Input {...props} bind:value={$formData.username} />
						{/snippet}
					</Form.Control>
					<Form.FieldErrors />
				</Form.Field>
				<Form.Field {form} name="placements">
					<Form.Control>
						{#snippet children({ props })}
							<SortableList
								data={data.tracks}
								prop={props}
								bind:value={$formData.placements}
							/>
						{/snippet}
					</Form.Control>
					<Form.FieldErrors />
				</Form.Field>
				<Form.Button class="h-14" variant="outline">Отправить оценки</Form.Button>
			</form>
		{:else}
			<p class="w-full max-w-4xl select-none text-center text-gray-500">{tracks}</p>
		{/if}
	{/await}
</div>
