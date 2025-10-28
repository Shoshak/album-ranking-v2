<script lang="ts">
	import { page } from '$app/state';
</script>

<div class="flex min-h-screen max-h-[calc(screen-)] items-center px-4 py-12 sm:px-6 md:px-8 lg:px-12 xl:px-16">
	<div class="w-full space-y-6 text-center">
		<div class="space-y-3">
			<h1 class="text-4xl font-bold tracking-tighter sm:text-5xl">{page.status}</h1>
			<p class="text-gray-500">{page.error?.message}</p>
		</div>
	</div>
</div>
