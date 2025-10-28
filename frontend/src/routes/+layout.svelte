<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import { ModeWatcher } from 'mode-watcher';
	import SunIcon from '@lucide/svelte/icons/sun';
	import MoonIcon from '@lucide/svelte/icons/moon';
	import { toggleMode } from 'mode-watcher';
	import { Button } from '$lib/components/ui/button/index.js';
	import { page } from '$app/state';

	let { data, children } = $props();

	let links = $state([
		{
			label: 'оценить альбом',
			href: '/rank-album'
		},
		{
			label: 'посмотреть оценки',
			href: '/check-rankings'
		}
	]);

	$effect(() => {
		if (data.user.admin_rights) {
			links = [
				{
					label: 'оценить альбом',
					href: '/rank-album'
				},
				{
					label: 'посмотреть оценки',
					href: '/check-rankings'
				},
				{
					label: 'добавить альбом',
					href: '/submit-album'
				},
				{
					label: 'добавить пользователя',
					href: '/submit-user'
				}
			];
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if !(page.url.pathname === '/')}
	<header
		class="bg-background dark:bg-input/30 mb-4 flex min-h-20 max-h-40 shrink-0 flex-row items-center px-6 shadow-sm"
	>
		<div class="flex items-center justify-start">
			<span
				class="transform-[translateY(-0.07em)] mr-10 flex h-full select-none text-4xl font-black"
				>album ranking.</span
			>

			<nav>
				{#each links as link}
					<a
						data-sveltekit-replacestate
						data-sveltekit-preload-data="tap"
						href={link.href}
						draggable="false"
						class="transform-[translateY(-0.07em)] inline-block h-full select-none items-center bg-transparent text-xl font-medium hover:bg-transparent hover:underline active:no-underline [&:not(:first-child)]:ml-6"
					>
						{link.label}</a
					>
				{/each}
			</nav>
		</div>
		<div class="ml-auto flex h-full items-center">
			<Button onclick={toggleMode} variant="ghost" size="icon">
				<SunIcon
					class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 !transition-all dark:-rotate-90 dark:scale-0"
				/>
				<MoonIcon
					class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 !transition-all dark:rotate-0 dark:scale-100"
				/>
			</Button>
		</div>
	</header>
{/if}
<Toaster />
<ModeWatcher />
{@render children?.()}
