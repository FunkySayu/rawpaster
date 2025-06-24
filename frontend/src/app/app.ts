import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FileListComponent } from './components/file-list/file-list'; // Adjusted path

@Component({
  selector: 'app-root',
  standalone: true, // Make AppComponent standalone
  imports: [RouterOutlet, FileListComponent], // Import FileListComponent
  templateUrl: './app.html',
  styleUrl: './app.css' // Assuming styleUrls for consistency, though styleUrl is for single
})
export class App { // Class name is App
  title = 'Flask Angular Paster'; // Updated title
}
