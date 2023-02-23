import { createAction, props } from '@ngrx/store';

export const SET_GRAPH_SEARCH = '[GRAPH] Set search query';

export const SetGraphSearch = createAction(
	SET_GRAPH_SEARCH,
	props<{
		payload: string
	}>()
)
