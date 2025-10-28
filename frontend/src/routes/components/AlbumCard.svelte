<script lang="ts">
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { ScrollArea } from '$lib/components/ui/scroll-area';
	import type { Ranking } from '../types';
	import * as Tooltip from '$lib/components/ui/tooltip/index.js';
	let { data } = $props();

	async function getRankings(): Promise<Ranking[] | string> {
		try {
			const response = await fetch('http://127.0.0.1:8000/rankings/' + data.id);
			const json = await response.json();
			return response.ok ? (json as Ranking[]) : (json.detail as string);
		} catch {
			return 'Что-то пошло не так.';
		}
	}

	let selectedAlbum: Promise<Ranking[] | string> = $state(new Promise(() => {}));
	let isRankingsDialogOpen: boolean = $state(false);
	let UserRankingDialog: { state: boolean; data: Ranking } = $state({
		state: false,
		data: { track_name: '', rankings: [], placement: 1 }
	});
	let tooltipEnabled: boolean = $state(false);

	function requestAlbum() {
		if (isRankingsDialogOpen) {
			selectedAlbum = getRankings();
		}
	}
	$effect(() => {
		if (UserRankingDialog.state) {
			setTimeout(() => {
				tooltipEnabled = true;
			}, 200);
		} else {
			tooltipEnabled = false;
		}
	});
</script>

<Dialog.Root bind:open={UserRankingDialog.state}>
	<Dialog.Content class="min-w-2xl [&>button]:hidden">
		<Dialog.Header>
			<Dialog.Title class="select-none">{UserRankingDialog.data.track_name}</Dialog.Title>
		</Dialog.Header>
		<div class="flex h-[600px] justify-items-center">
			<ScrollArea class="h-[600px] w-full p-4">
				<div class="justify-items-left grid grid-cols-2 gap-5">
					{#each UserRankingDialog.data.rankings as ranking}
						<div
							class="bg-background dark:border-input flex h-12 w-24 select-none items-center overflow-hidden rounded-lg border"
						>
							<Tooltip.Provider disabled={!tooltipEnabled}>
								<Tooltip.Root delayDuration={700}>
									<Tooltip.Trigger>
										<img
											class="pointer-events-none h-12 w-12"
											loading="lazy"
											src={`/${ranking.username}.jpg`}
											alt={ranking.username}
										/>
									</Tooltip.Trigger>
									<Tooltip.Content
										arrowClasses="hidden"
										sideOffset={8}
										class="bg-background text-primary shadow-xs select-none border text-xs"
									>
										{ranking.username}
									</Tooltip.Content>
								</Tooltip.Root>
							</Tooltip.Provider>
							<div
								class="dark:border-input flex h-12 w-12 items-center justify-center border-r text-4xl"
							>
								{ranking.placement}
							</div>
						</div>
					{/each}
				</div>
			</ScrollArea>
		</div>
	</Dialog.Content>
</Dialog.Root>

<Dialog.Root bind:open={isRankingsDialogOpen} onOpenChange={requestAlbum}>
	<Dialog.Trigger>
		<div
			class="shadow-accent hover:transform-[scale(1.03)] duration-50 cursor-pointer overflow-hidden rounded-lg border-4 shadow-lg transition-all ease-in"
		>
			<img alt={data.name} src={data.cover} class="pointer-events-none select-none" />
		</div>
	</Dialog.Trigger>
	<Dialog.Content class="min-w-3xl [&>button]:hidden">
		<Dialog.Header>
			<Dialog.Title class="select-none">{data.artist + ' - ' + data.name}</Dialog.Title>
		</Dialog.Header>
		<div class="flex h-[600px] justify-center">
			{#await selectedAlbum then rankings}
				{#if !(typeof rankings === 'string')}
					<ScrollArea class="h-[600px] w-full p-4">
						<div
							class="bg-background dark:border-input select-none overflow-hidden rounded-lg border"
						>
							{#each rankings as ranking, i}
								<div
									role="button"
									tabindex={i}
									onkeydown={() => {}}
									class="bg-background hover:bg-accent dark:bg-input/30 dark:border-input dark:hover:bg-input/50 flex h-12 cursor-pointer [&:not(:last-child)]:border-b"
									onclick={() => {
										isRankingsDialogOpen = !isRankingsDialogOpen;
										UserRankingDialog = {
											state: !UserRankingDialog.state,
											data: ranking
										};
									}}
								>
									<div
										class="hover:text-accent-foreground dark:border-input flex h-12 w-12 items-center justify-center border-r text-xl"
									>
										{i + 1}
									</div>
									<div
										class="hover:text-accent-foreground dark:border-input flex h-12 w-12 items-center justify-center border-r text-xl"
									>
										{ranking.placement}
									</div>
									<div
										class="hover:text-accent-foreground flex items-center pl-4"
									>
										{ranking.track_name}
									</div>
								</div>
							{/each}
						</div>
					</ScrollArea>
				{:else}
					<p class="flex select-none text-center text-gray-500">
						{rankings}
					</p>
				{/if}
			{/await}
		</div>
	</Dialog.Content>
</Dialog.Root>
