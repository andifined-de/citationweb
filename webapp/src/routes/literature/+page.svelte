<script lang="ts">
	import { onMount } from 'svelte';
	import Sigma from "sigma";
	import Graph from 'graphology';
import seedrandom from "seedrandom";

import EdgesDefaultProgram from "sigma/rendering/webgl/programs/edge";
import EdgesFastProgram from "sigma/rendering/webgl/programs/edge.fast";

import circular from 'graphology-layout/circular';
import FA2Layout from "graphology-layout-forceatlas2/worker";
import forceAtlas2 from "graphology-layout-forceatlas2";

	let canvas: HTMLCanvasElement;
	let container: HTMLElement;

	const rng = seedrandom("sigma");
	const graph = new Graph({multi: true, allowSelfLoops: true, type: 'directed'});

	onMount(() => {
		container = document.getElementById("sigma-container") as HTMLElement;
		//const graph = new Graph({type: 'directed'});
		const fa2Button = document.getElementById("fa2") as HTMLButtonElement;

		/*const renderer = new Sigma(graph, container, {
			defaultEdgeColor: "#e6e6e6",
			defaultEdgeType: 'edges-fast',
		});*/

		(async () => {
			const data = await fetchCitations();
			console.log(data);
			graph.import(data);
			console.log(graph);
			circular.assign(graph);
			const sensibleSettings = forceAtlas2.inferSettings(graph);
			const fa2Layout = new FA2Layout(graph, {
				settings: sensibleSettings,
			});
			// Cheap trick: tilt the camera a bit to make labels more readable:
			const renderer = new Sigma(graph, container);
			renderer.getCamera().setState({
				angle: 0.2,
			});

			function toggleFA2Layout() {
				if (fa2Layout.isRunning()) {
					fa2Layout.stop();
					fa2Button.innerHTML = `Start layout ▶`;
				} else {
					fa2Layout.start();
					fa2Button.innerHTML = `Stop layout ⏸`;
				}
			}
			fa2Button.addEventListener("click", toggleFA2Layout);
		})();
	});

	const fetchCitations = async () => {
		let currentEdgeIndex = 0;
		const nodes = new Map<string, any>();
		const edges = new Map<string, any>();

		const response = await fetch('http://localhost:8000/citations');
		const citations: any[] = await response.json();
		/**
		 * {
      "key": "1.0",
      "attributes": {
        "x": 296.39902,
        "y": 57.118374,
        "size": 15,
        "label": "Napoleon",
        "color": "#B30000"
      }
    },
		*/

		citations.forEach((citation) => {
			nodes.set(citation.cited.id, {
				key: citation.cited.id,
				attributes: {
					label: citation.cited.title,
				}
			});
			nodes.set(citation.citing.id, {
				key: citation.citing.id,
				attributes: {
					label: citation.citing.title,
				}
			});
			edges.set(`e${currentEdgeIndex}`, {
				key: `e${currentEdgeIndex}`,
				source: citation.citing.id,
				target: citation.cited.id,
				type: 'arrow'
			})
			currentEdgeIndex++;
		})
		console.log(edges);
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
<div id="sigma-container"></div>
<button id="fa2"></button>
<style>
	.network-graph, #sigma-container {
		width: 100vw;
		height: 100vh;
		position: absolute;
		top: 0;
		left: 0;
	}

	button {
		position: absolute;
		z-index: 99;
	}
</style>
