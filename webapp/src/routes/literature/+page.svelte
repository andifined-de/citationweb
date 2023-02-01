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
	import type { EdgeDisplayData, NodeDisplayData } from 'sigma/types';

	interface State {
		hoveredNode?: string;
		hoveredNeighbors?: Set<string>;
		selectedNode?: string;
	}
	const state: State = {};


	let canvas: HTMLCanvasElement;
	let container: HTMLElement;

	const graph = new Graph({multi: true, allowSelfLoops: true, type: 'directed'});

	onMount(() => {
		container = document.getElementById("sigma-container") as HTMLElement;
		const fa2Button = document.getElementById("fa2") as HTMLButtonElement;

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

			// Bind graph interactions:
			renderer.on("enterNode", ({ node }) => {
				setHoveredNode(renderer, node);
			});
			renderer.on("leaveNode", () => {
				setHoveredNode(renderer, undefined);
			});


			// Render nodes accordingly to the internal state:
			// 1. If a node is selected, it is highlighted
			// 2. If there is a hovered node, all non-neighbor nodes are greyed
			renderer.setSetting("nodeReducer", (node, data) => {
				const res: Partial<NodeDisplayData> = { ...data };

				if (!state.hoveredNode) {
					res.label = '';
				}

				if (state.hoveredNeighbors && !state.hoveredNeighbors.has(node) && state.hoveredNode !== node) {
					res.label = '';
					res.color = 'rgba(190,190,190,0.2)';
				}

				if (state.selectedNode === node) {
					res.highlighted = true;
					res.color = 'rgba(102,178,178, 1)';
				}
				return res;
			});

			// Render edges accordingly to the internal state:
			// 1. If a node is hovered, the edge is hidden if it is not connected to the
			//    node
			// 2. If there is a query, the edge is only visible if it connects two
			//    suggestions
			renderer.setSetting("edgeReducer", (edge, data) => {
				const res: Partial<EdgeDisplayData> = { ...data };

				if (state.hoveredNode && !graph.hasExtremity(edge, state.hoveredNode)) {
					res.hidden = true;
				}

				return res;
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

		const response = await fetch('http://localhost:8000/api/v1/citations');
		const citations: any[] = await response.json();

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

	function setHoveredNode(renderer: Sigma, node?: string) {
		if (node) {
			state.hoveredNode = node;
			state.hoveredNeighbors = new Set(graph.neighbors(node));
		} else {
			state.hoveredNode = undefined;
			state.hoveredNeighbors = undefined;
		}

		// Refresh rendering:
		renderer.refresh();
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
