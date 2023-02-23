import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable, map } from 'rxjs';
import { environment } from 'src/environments/environment';
import { GraphState } from '../store/graph.state';
import { SET_GRAPH_SEARCH, SetGraphSearch } from '../store/graph.actions';
import { getGraph } from '../store/graph.selectors';

@Injectable()
export class GraphDataService {
	constructor(protected http: HttpClient, protected store: Store<GraphState>) {}

	setSearchQuery(query: string) {
		this.store.dispatch(SetGraphSearch({payload: query}))
	}

	getSearchQuery(): Observable<string> {
		return this.store.select(getGraph).pipe(
			map((s) => s.search)
		)
	}

	searchLiterature(query: string): Observable<any> {
		return this.http.get(`${environment.backend}/citations/search`, {params: {
			q: query
		}}).pipe(
			map((citations) => {
				let currentEdgeIndex = 0;
				const nodes = new Map<string, any>();
				const edges = new Map<string, any>();
				(<any[]>citations).forEach((citation) => {
					nodes.set(citation.cited.id, {
						key: citation.cited.id,
						attributes: {
							label: citation.cited.title,
							size: Math.log(citation.cited.citation_score)
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
				return {nodes: Array.from(nodes.values()), edges: Array.from(edges.values())}
			})
		)
	}
}
