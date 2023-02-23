import { createFeatureSelector, createSelector } from '@ngrx/store';
import { GraphState } from './graph.state';

export const GRAPH_STATE_FEATURE = 'graph';

export const getGraphState = createFeatureSelector<GraphState>(GRAPH_STATE_FEATURE);

export const getGraph = createSelector(getGraphState, (state: GraphState) => state);
