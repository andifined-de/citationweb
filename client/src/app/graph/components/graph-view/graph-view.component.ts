import { Component, ElementRef, OnDestroy, OnInit, ViewChild } from '@angular/core';
import Graph from 'graphology';
import { map, mergeMap, of, tap } from 'rxjs';
import Sigma from 'sigma';
import { GraphDataService } from '../../services/graph-data.service';
import circlepack from 'graphology-layout/circlepack';
import FA2Layout from "graphology-layout-forceatlas2/worker";
import forceAtlas2 from "graphology-layout-forceatlas2";
import { EdgeDisplayData, NodeDisplayData } from 'sigma/types';

interface State {
	hoveredNode?: string;
	hoveredNeighbors?: Set<string>;
	selectedNode?: string;
}

@Component({
  selector: 'app-graph-view',
  templateUrl: './graph-view.component.html',
  styleUrls: ['./graph-view.component.scss']
})
export class GraphViewComponent implements OnInit, OnDestroy {

	state: State = {};

  @ViewChild("sigmaContainer") container?: ElementRef;
  sigma?: Sigma;
  graph: Graph = new Graph({multi: true, allowSelfLoops: true, type: 'directed'});
	layout = new FA2Layout(this.graph, {
		settings: {
			barnesHutOptimize: true,
		},
	})
	layoutRunning = false;

  constructor(protected graphDataService: GraphDataService) { }

	toggleLayout(): void {
		if (this.layout.isRunning()) {
			this.layout.stop();
		} else {
			this.layout.start();
		}
	}

	protected setHoveredNode(renderer: Sigma, node?: string) {
		if (node) {
			this.state.hoveredNode = node;
			this.state.hoveredNeighbors = new Set(this.graph.neighbors(node));
		} else {
			this.state.hoveredNode = undefined;
			this.state.hoveredNeighbors = undefined;
		}

		// Refresh rendering:
		renderer.refresh();
	}

  ngOnInit(): void {
		this.graphDataService.getSearchQuery().pipe(
			tap(console.log),
			mergeMap((q) => {
				if (q?.length === 0) return of(null);
				return this.graphDataService.searchLiterature(q).pipe(
					map((data) => {
						this.layout.stop();
						this.graph.clear();
						this.graph.import(data);
						circlepack.assign(this.graph);
						this.layout.start();
						setTimeout(() => this.layout.stop(), 3000);
					})
				)
				})
		)
    .subscribe();
  }

  ngAfterViewInit(): void {
    if(!!this.container) {
      this.sigma = new Sigma(this.graph, this.container?.nativeElement, {
				defaultNodeColor: '#36c9c9',
				defaultEdgeColor: '#36c9c9',
				allowInvalidContainer: true
			});
			this.sigma.getCamera().setState({
				angle: 0.2,
			});
			this.sigma.on('enterNode', ({ node }) => {
				!!this.sigma && this.setHoveredNode(this.sigma, node);
			});
			this.sigma.on('leaveNode', () => {
				!!this.sigma && this.setHoveredNode(this.sigma, undefined);
			});
			this.sigma.setSetting("nodeReducer", (node, data) => {
				const res: Partial<NodeDisplayData> = { ...data };

				// res.size = graph.neighbors(node).length + 1;
				if (!this.state.hoveredNode) {
					res.label = '';
				}

				if (this.state.hoveredNeighbors && !this.state.hoveredNeighbors.has(node) && this.state.hoveredNode !== node) {
					res.label = '';
					res.color = 'hsl(208, 33%, 20%)';
				}

				if (this.state.hoveredNeighbors && this.state.hoveredNeighbors.has(node)) {
					res.highlighted = true;
				}

				if (this.state.selectedNode === node) {
					res.highlighted = true;
					res.color = '#44dbdb';
				}
				return res;
			});
			this.sigma.setSetting("edgeReducer", (edge, data) => {
				const res: Partial<EdgeDisplayData> = { ...data };

				if (!this.state.hoveredNode) {
					res.hidden = true;
				}

				if (this.state.hoveredNode && !this.graph.hasExtremity(edge, this.state.hoveredNode)) {
					res.hidden = true;
				}

				return res;
			});
    }
  }

  ngOnDestroy(): void {
    !!this.sigma && this.sigma.kill;
  }

}
