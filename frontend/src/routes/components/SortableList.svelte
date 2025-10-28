<script lang="ts">
	import Sortable from 'sortablejs';
	import { onMount } from 'svelte';
	import type { Track } from '../types';

	const useSortable = (getter: () => HTMLElement | null, options?: Sortable.Options) => {
		$effect(() => {
			const sortableEl = getter();
			const sortable = sortableEl ? Sortable.create(sortableEl, options) : null;
			return () => sortable;
		});
	};

	let { data, value = $bindable([]), prop } = $props();

	let sortable = $state<HTMLElement | null>(null);

	async function getTracks() {
		return data;
	}
	onMount(() => {
		getTracks().then((tracks) => {
			value = tracks.map((track: Track) => track.id);
		});

		useSortable(() => sortable, {
			animation: 100,
			chosenClass: 'sortable-ghost',
			onEnd(evt) {
				let ids = [];
				const children = evt.target.children;
				let i = 1;
				for (let item of children) {
					const string_id = item.getAttribute('data-id');
					ids.push(parseInt(!(string_id === null) ? string_id : ''));
					item.children[0].innerHTML = i.toString();
					i++;
				}
				value = ids;
			}
		});
	});
</script>

<input class="invisible hidden" bind:value {...prop} />
{#await data then tracks}
	<div class="pb-2 pt-2">
		<div class="bg-background dark:border-input select-none overflow-hidden rounded-lg border">
			<div bind:this={sortable}>
				{#each tracks as track, i}
					<div
						data-id={i + 1}
						class="bg-background hover:bg-accent dark:bg-input/30 dark:border-input dark:hover:bg-input/50 flex min-h-12 cursor-grab items-center [&:not(:last-child)]:border-b"
					>
						<div
							class="hover:text-accent-foreground dark:border-input flex min-h-12 min-w-12 select-none items-center justify-center self-stretch border-r text-xl"
						>
							{i + 1}
						</div>
						<div class="hover:text-accent-foreground flex h-full select-none pl-4">
							{track.track_name}
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
{/await}
