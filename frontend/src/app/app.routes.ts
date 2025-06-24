import { Routes } from '@angular/router';
import { FileListComponent } from './components/file-list/file-list';
import { AddFileComponent } from './components/add-file/add-file';

export const routes: Routes = [
  { path: '', redirectTo: '/files', pathMatch: 'full' }, // Default route
  { path: 'files', component: FileListComponent },
  { path: 'add', component: AddFileComponent },
  // Potentially a catch-all or Not Found component here later
  // { path: '**', component: PageNotFoundComponent },
];
