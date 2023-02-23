import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { GraphDataService } from '../../services/graph-data.service';

@Component({
  selector: 'app-graph-header',
  templateUrl: './graph-header.component.html',
  styleUrls: ['./graph-header.component.scss']
})
export class GraphHeaderComponent {

  searchForm = new FormGroup({
		query: new FormControl('')
	})

  constructor(protected graphDataService: GraphDataService) { }

	onSearchSubmit() {
		console.log('submit');
		this.graphDataService.setSearchQuery(this.searchForm.controls.query.value || '');
	}
}
