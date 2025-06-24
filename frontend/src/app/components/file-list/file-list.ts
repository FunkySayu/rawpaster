import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // Required for *ngFor, async pipe, etc.
import { ApiService, ApiFile } from '../../services/api';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-file-list',
  standalone: true, // Ensure it's a standalone component
  imports: [CommonModule], // Add CommonModule here for async pipe and ngFor
  templateUrl: './file-list.html',
  styleUrls: ['./file-list.css'] // Corrected to styleUrls
})
export class FileListComponent implements OnInit { // Changed class name to FileListComponent for consistency
  files$: Observable<ApiFile[]> | undefined;
  error: string | null = null;

  // Variable to store selected file content
  selectedFileContent: string | null = null;
  selectedFilePath: string | null = null;

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    this.loadFiles();
  }

  loadFiles(): void {
    this.error = null;
    this.selectedFileContent = null;
    this.selectedFilePath = null;
    // Note: Ensure ApiService has a valid API key for this to work.
    // You might need to add a dummy key to authorized_keys.txt and set it in ApiService.
    // For example, add 'testkey' to 'authorized_keys.txt' and update ApiService.apiKey = 'testkey';
    this.files$ = this.apiService.getFiles();
    this.files$.subscribe({
      error: (err) => {
        console.error('Error loading files:', err);
        let errorMessage = `Failed to load files. Server: ${err.message || 'Unknown error'}`;
        if (err.status === 401) {
          errorMessage += " (Unauthorized - Check API Key in ApiService and ensure it's in authorized_keys.txt on server)";
        } else if (err.status === 0) {
          errorMessage += " (Could not connect to API - Is the backend running and Nginx proxying correctly?)";
        }
        this.error = errorMessage;
      }
    });
  }

  viewFile(file: ApiFile): void {
    this.selectedFilePath = file.path;
    this.selectedFileContent = 'Loading...';
    this.apiService.getFileContent(file.path).subscribe({
      next: (content) => {
        this.selectedFileContent = content;
      },
      error: (err) => {
        console.error('Error loading file content:', err);
        this.selectedFileContent = `Failed to load file content: ${err.message}`;
      }
    });
  }
}
