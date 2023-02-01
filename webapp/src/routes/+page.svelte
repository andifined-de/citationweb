<script lang="ts">
	import { onMount } from 'svelte';
	import { Graph } from '@cosmograph/cosmos';

	let container: HTMLElement;
	let canvas: HTMLCanvasElement;

	const defaults = {
		nodeColor: '#00897b',
		adjacentNodeColor: '#00564d',
		linkColor: '#969696'
	}
	const config = {
		simulation: {
			repulsion: 2,
			linkSpring: 2,
			gravity: 0.1
		},
		renderLinks: true,
		linkGreyoutOpacity: 0.05,
		linkColor: link => link.color || defaults.linkColor,
		nodeColor: node => node.color || defaults.nodeColor,
		backgroundColor: '#282828',
		nodeSize: node => node.size || 1,
	}


	onMount(() => {
		let graph: any;

		//const graph = new Graph({type: 'directed'});

		(async () => {
			const data = await fetchCitations();
			console.log(data)
			graph = new Graph(canvas, config);
			graph.setConfig({
				events: {
					onClick: node => {
						highlightSelectedNodes(graph, node)
						console.log('Clicked node: ', node)
					},
				},
			});
			graph.setData(data.nodes, data.edges)
		})();
	});

	const fetchCitations = async () => {
		let currentEdgeIndex = 0;
		const nodes = new Map<string, any>();
		const edges = new Map<string, any>();

		const response = await fetch('http://localhost:8000/api/v1citations');
		const citations: any[] = await response.json();

		citations.forEach((citation) => {
			nodes.set(citation.cited.id, {
				id: citation.cited.id,
				//label: citation.source.title,
				size: citation.cited.citation_score
			});
			nodes.set(citation.citing.id, {
				id: citation.citing.id,
				//label: citation.referencing_paper.title,
				size: citation.citing.citation_score
			});
			edges.set(`e${currentEdgeIndex}`, {
				id: `e${currentEdgeIndex}`,
				source: citation.citing.id,
				target: citation.cited.id,
				type: 'arrow',
			})
			currentEdgeIndex++;
		})
		return {nodes: Array.from(nodes.values()), edges: Array.from(edges.values())}
	};

	const highlightSelectedNodes = (graph: any, node: any) => {
		if (!!graph) {
			graph.unselectNodes()
			const nodes = graph.getAdjacentNodes(node.id);
			graph.selectNodesByIds([node.id , ...nodes.map((n) => n.id)]); // Select adjacent nodes
		}
	}
</script>

<svelte:head>
	<title>Citation Web</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<canvas class="network-graph" bind:this={canvas}></canvas>

<style>
	.network-graph {
		width: 100vw;
		height: 100vh;
		position: absolute;
		top: 0;
		left: 0;
	}
</style>
