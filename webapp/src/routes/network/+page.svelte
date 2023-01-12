<script lang="ts">
	import Sigma from "sigma";
	import Graph, { DirectedGraph } from 'graphology';
	import circular from 'graphology-layout/circular';
	import random from 'graphology-layout/random';
	import {assignLayout} from 'graphology-layout/utils';
	import { onMount } from 'svelte';
	//import forceLayout from 'graphology-layout-force';
	import forceAtlas2 from 'graphology-layout-forceatlas2';
	import louvain from 'graphology-communities-louvain';
	import FA2Layout from 'graphology-layout-forceatlas2/worker';


/*
	const data = {
		"nodes": [
			{
				"key": "n0",
				"label": "A node",
				"size": 30
			},
			{
				"key": "n1",
				"label": "Another node",
				"size": 2
			},
		],
		"edges": [
			{
				"key": "e0",
				"source": "n0",
				"target": "n1",
				value: 'KNOWS',
				weight: 2
			},
		]
	}
*/

	let container: HTMLElement;
	let layout: FA2Layout;

	onMount(() => {
		//const graph = new Graph({type: 'directed'});

		(async () => {
				const data = await fetchCitations();
				console.log(data)
				const graph = DirectedGraph.from(data);
				const positions = circular(graph);
				//const positions = forceLayout(graph, {maxIterations: 50})
				//circular.assign(graph);
				assignLayout(graph, positions, {dimensions: ['x', 'y']});
				layout = new FA2Layout(graph, {
					settings: {gravity: 1},
					iterations: 3,
					barnesHutOptimize: true
				});
				layout.start();
				//louvain.assign(graph)
				//forceLayout.assign(graph, 50);
				const s = new Sigma(graph, container, {
					renderLabels: true,
					renderEdgeLabels: true,
					defaultNodeColor: '#ff0000',
				});

				s.on('clickNode', (e) => {
					highlightConnected(e, graph);
					showTitle(e, graph);
				});
		})();
	});

	const fetchCitations = async () => {
		let currentEdgeIndex = 0;
		const nodes = new Map<string, any>();
		const edges = new Map<string, any>();

		const response = await fetch('http://localhost:8000/citations');
		const citations: any[] = await response.json();

		citations.forEach((citation) => {
			nodes.set(citation.source_id, {
				key: citation.source_id,
				label: citation.source.title || 'hallo',
			});
			nodes.set(citation.referencing_id, {
				key: citation.referencing_id,
				label: citation.referencing_paper.title || 'hallo',
			});
			edges.set(`e${currentEdgeIndex}`, {
				key: `e${currentEdgeIndex}`,
				source: citation.referencing_id,
				target: citation.source_id,
				type: 'arrow',
				label: 'test'
			})
			currentEdgeIndex++;
		})
		console.log(citations);
		return {nodes: Array.from(nodes.values()), edges: Array.from(edges.values())}
	};

	const highlightConnected = (event: any, graph: Graph) => {
		console.log(event)
		//const neighbours = graph.filterEdges()
		//console.log(neighbours)
	}

	const showTitle = async (event: any, graph: Graph) => {
		const node = event.node;
		const response = await fetch(`http://localhost:8000/literature/${node}`);
		const literature: {title: string} = await response.json();
		console.log(literature)
	}

	const handleStop = () => {
		if (!!layout) layout.stop()
	}
</script>

<svelte:head>
	<title>Citation Web</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h1>Citation Web</h1>
	<button on:click={handleStop}>Stop simulation</button>
	<div class="network-container"  bind:this={container}></div>
</section>

<style>
	section, div {
		height: 100%;
		width: 100%;
	}
</style>
