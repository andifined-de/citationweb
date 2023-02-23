import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GraphHeaderComponent } from './components/graph-header/graph-header.component';
import { GraphViewComponent } from './components/graph-view/graph-view.component';
import { GraphSettingsComponent } from './components/graph-settings/graph-settings.component';
import { HttpClientModule } from '@angular/common/http';
import { GraphDataService } from './services/graph-data.service';
import { StoreModule } from '@ngrx/store';
import { GRAPH_STATE_FEATURE } from './store/graph.selectors';
import { graphReducer } from './store/graph.reducer';
import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    GraphSettingsComponent,
    GraphHeaderComponent,
    GraphViewComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule,
    ReactiveFormsModule,
    StoreModule.forFeature(GRAPH_STATE_FEATURE, graphReducer),
  ],
  exports: [
    GraphSettingsComponent,
    GraphHeaderComponent,
    GraphViewComponent,
  ],
  providers: [
    {
      provide: GraphDataService,
      useClass: GraphDataService
    }
  ]
})
export class GraphModule { }
