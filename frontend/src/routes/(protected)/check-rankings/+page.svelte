<script lang="ts">
	import type { PageProps } from './$types';
	import { ScrollArea } from '$lib/components/ui/scroll-area/index.js';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import AlbumCard from '../../components/AlbumCard.svelte';

	let { data }: PageProps = $props();
</script>

<div class="flex h-[800px] flex-col items-center space-y-4 p-2">
	{#await data.albums}
		<Skeleton class="bg-background dark:bg-input/30 w-4xl h-full rounded-lg " />
	{:then albums}
		{#if !(typeof albums === 'string')}
			<ScrollArea class="w-4xl h-full rounded-md border p-8">
				<div role="grid" class="grid grid-cols-4 items-center gap-20 p-10">
					{#each albums as album, i}
						{console.log(album)}
						<AlbumCard data={album} />
					{/each}
				</div>
			</ScrollArea>
		{:else}
			<p class="w-full max-w-4xl select-none text-center text-gray-500">{albums}</p>
		{/if}
	{/await}
</div>
