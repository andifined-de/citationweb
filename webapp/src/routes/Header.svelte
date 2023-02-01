<script>
	import { page } from '$app/stores';
	import logo from '$lib/images/svelte-logo.svg';
	import github from '$lib/images/github.svg';
</script>

<header>
	<h1>Citation Web</h1>
</header>

<style>
	header {
		display: flex;
		justify-content: space-between;
	}

	header h1 {
		display: flex;
		align-items: center;
		justify-content: center;
		position: fixed;
		inset: 0;
		font-size: 14vw;
		text-transform: uppercase;
	}
</style>
