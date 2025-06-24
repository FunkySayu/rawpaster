import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

// Define an interface for the file item
export interface ApiFile {
  timestamp: number;
  path: string;
}

@Injectable({
  providedIn: 'root'
})
export class Api {
  private apiUrl = '/api'; // Nginx will proxy this

  // You'll need to get the API key from somewhere (e.g., user input, config)
  // For now, let's hardcode a placeholder or assume it's passed if needed.
  // The /api/list endpoint requires a 'key' query parameter.
  private apiKey = 'testkey123'; // Using the key from authorized_keys.txt

  constructor(private http: HttpClient) { }

  getFiles(): Observable<ApiFile[]> {
    // The backend /api/list expects a 'key' query parameter
    // For testing, you might need to replace 'YOUR_API_KEY_HERE'
    // or implement a way for the user to provide it.
    // If your actual 'authorized_keys.txt' is empty or has no valid keys,
    // this request will fail with a 401.
    // Make sure to populate 'authorized_keys.txt' with at least one key.
    // For example, add 'testkey' to 'authorized_keys.txt'.
    // Then, set this.apiKey = 'testkey';

    // If config.master_key is needed for some operations, ensure it's also set.

    const headers = new HttpHeaders({
      // 'Authorization': `Bearer ${this.apiKey}` // If using Bearer token auth
      // Add any other headers if required by your API
    });

    // The key must be provided as a query parameter for the /api/list endpoint
    return this.http.get<ApiFile[]>(`${this.apiUrl}/list?key=${this.apiKey}`, { headers });
  }

  // Placeholder for fetching file content
  getFileContent(filePath: string): Observable<string> {
    // The backend /api/files/<fileid> does not explicitly require a key in its path definition
    // but the underlying file access logic might still depend on authorized keys.
    // The current Flask implementation for /api/files/<fileid> iterates through all authorized keys
    // to find the file. This means the file must exist under one of the key-specific folders.
    // No explicit 'key' query param is needed for this specific endpoint call,
    // as long as the file can be resolved through one of the authorized key paths.
    return this.http.get(filePath, { responseType: 'text' }); // filePath is already /api/files/...
  }

  // Placeholder for adding content
  addFile(content: string): Observable<{ path: string }> {
    // The /api/add endpoint requires a 'key' query parameter.
    const headers = new HttpHeaders({
      'Content-Type': 'text/plain' // Or 'application/octet-stream' depending on backend
    });
    return this.http.post<{ path: string }>(`${this.apiUrl}/add?key=${this.apiKey}`, content, { headers });
  }
}
