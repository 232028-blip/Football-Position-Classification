import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface PredictionResponse {
  prediction: string;
  task: string;
  model_name: string;
  classes: string[];
  probabilities?: number[];
  disclaimer: string;
}

@Injectable({ providedIn: 'root' })
export class PredictionService {
  private readonly http = inject(HttpClient);

  predict(payload: Record<string, number | null>): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>('/api/predict', payload);
  }

  example(): Observable<Record<string, number>> {
    return this.http.get<Record<string, number>>(`${document.baseURI}sample-player.json`);
  }
}
