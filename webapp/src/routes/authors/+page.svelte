<script lang="ts">
	import { onMount } from 'svelte';
	import Sigma from "sigma";
import Graph from "graphology";

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


	let container: HTMLElement;

	const graph = new Graph({
		defaultEdgeArrow: 'source'
	});

	// Type and declare internal state:


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
			const renderer = new Sigma(graph, container, {
				defaultEdgeType: 'arrow',
			});
			renderer.getCamera().setState({
				angle: 0.2,
			})

			// Bind graph interactions:
			renderer.on("enterNode", ({ node }) => {
				setHoveredNode(renderer, node);
			});
			renderer.on("leaveNode", () => {
				setHoveredNode(renderer, undefined);
			});


			// Render nodes accordingly to the internal state:
			// 1. If a node is selected, it is highlighted
			// 2. If there is query, all non-matching nodes are greyed
			// 3. If there is a hovered node, all non-neighbor nodes are greyed
			renderer.setSetting("nodeReducer", (node, data) => {
				console.log('nodereducer', state.selectedNode, node);
				const res: Partial<NodeDisplayData> = { ...data };

				if (state.hoveredNeighbors && !state.hoveredNeighbors.has(node) && state.hoveredNode !== node) {
					res.label = "";
					res.color = "#f6f6f6";
				}

				if (state.selectedNode === node) {
					res.highlighted = true;
				}
				return res;
			});

			// Render edges accordingly to the internal state:
			// 1. If a node is hovered, the edge is hidden if it is not connected to the
			//    node
			// 2. If there is a query, the edge is only visible if it connects two
			//    suggestions
			renderer.setSetting("edgeReducer", (edge, data) => {
				console.log('edgereducer', edge);
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

		const response = await fetch('http://localhost:8000/api/v1/author-citations');
		const citations: any[] = await response.json();

		citations.forEach((citation) => {
			nodes.set(citation.cited_id, {
				key: citation.cited_id,
				attributes: {
					label: citation.cited_name,
				}
			});
			nodes.set(citation.citing_id, {
				key: citation.citing_id,
				attributes: {
					label: citation.citing_name,
				}
			});
			edges.set(`e${currentEdgeIndex}`, {
				key: `e${currentEdgeIndex}`,
				source: citation.citing_id,
				target: citation.cited_id,
			})
			currentEdgeIndex++;
		})
		console.log(edges);
		return {nodes: Array.from(nodes.values()), edges: Array.from(edges.values())}
	};

	function setHoveredNode(renderer: Sigma, node?: string) {
		console.log('sethoverednode', node);
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
