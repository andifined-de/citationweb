import { createReducer, on } from '@ngrx/store'
import { SetGraphSearch } from './graph.actions';
import { GraphState } from './graph.state';

const initialState: GraphState = {
	search: ''
}

export const graphReducer = createReducer(
	initialState,
	on(SetGraphSearch, (state, { payload }) => {
		return {
			...state,
			search: payload
		};
	})
)
