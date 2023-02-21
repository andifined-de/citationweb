<script>
	import Header from './Header.svelte';
	import './styles.css';
</script>

<div class="app">

	<Header />
	<main>
		<slot />
	</main>

</div>

<style>
	.app {
		display: grid;
		min-height: 100vh;
		grid-template-rows: min-content 1fr min-content;
	}

	main {
		align-self: stretch;
	}

</style>
