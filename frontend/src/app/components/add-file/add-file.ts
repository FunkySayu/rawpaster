import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; // Required for ngModel
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';
import { FileListComponent } from '../file-list/file-list'; // To call refresh

@Component({
  selector: 'app-add-file',
  standalone: true,
  imports: [FormsModule, CommonModule], // Import FormsModule for ngModel
  templateUrl: './add-file.html',
  styleUrls: ['./add-file.css'] // Corrected to styleUrls
})
export class AddFileComponent { // Renamed class for consistency
  fileContent: string = '';
  statusMessage: string | null = null;
  messageIsError: boolean = false;

  constructor(private apiService: ApiService) { }

  addFile(): void {
    if (!this.fileContent.trim()) {
      this.statusMessage = 'Content cannot be empty.';
      this.messageIsError = true;
      return;
    }

    this.statusMessage = 'Adding file...';
    this.messageIsError = false;

    this.apiService.addFile(this.fileContent).subscribe({
      next: (response) => {
        this.statusMessage = `File added successfully! Path: ${response.path}`;
        this.messageIsError = false;
        this.fileContent = ''; // Clear textarea
        // Optionally, refresh the file list if it's displayed on the same page
        // This requires a way to communicate between components or a shared state management.
        // For simplicity, we'll assume the user can manually refresh the list for now,
        // or we could pass an event emitter if FileListComponent is a parent/sibling.
      },
      error: (err) => {
        console.error('Error adding file:', err);
        this.statusMessage = `Failed to add file: ${err.message || 'Unknown error'}`;
        if (err.status === 401) {
            this.statusMessage += " (Unauthorized - Check API Key in ApiService)";
        }
        this.messageIsError = true;
      }
    });
  }
}
