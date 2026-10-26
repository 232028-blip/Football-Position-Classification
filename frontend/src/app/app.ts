import { CommonModule } from '@angular/common';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FEATURES } from './feature-schema';
import { PredictionResponse, PredictionService } from './prediction.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  readonly fields = FEATURES;
  readonly groups = [...new Set(FEATURES.map(field => field.group))];
  readonly staticDemo = !['localhost', '127.0.0.1'].includes(window.location.hostname);
  values: Record<string, number | null> = Object.fromEntries(FEATURES.map(field => [field.name, null]));
  loading = false;
  error = '';
  result: PredictionResponse | null = null;
  private readonly api = inject(PredictionService);

  fieldsIn(group: string) {
    return this.fields.filter(field => field.group === group);
  }

  loadExample(): void {
    this.error = '';
    this.api.example().subscribe({
      next: sample => {
        this.values = Object.fromEntries(this.fields.map(field => [field.name, sample[field.name] ?? null]));
      },
      error: () => this.error = 'Example player could not be loaded.',
    });
  }

  submit(): void {
    this.error = '';
    this.result = null;
    if (this.staticDemo) {
      this.error = 'Static GitHub Pages demonstration: start Angular and Flask locally for predictions.';
      return;
    }
    const payload: Record<string, number | null> = {};
    for (const field of this.fields) {
      const value = this.values[field.name];
      if (value === null || value === undefined) {
        if (!field.required) { payload[field.name] = null; continue; }
        this.error = `Enter a value for ${field.label}.`;
        return;
      }
      if (!Number.isFinite(Number(value))) {
        this.error = `Enter a valid number for ${field.label}.`;
        return;
      }
      const numeric = Number(value);
      if (numeric < field.min || numeric > field.max) {
        this.error = `${field.label} must be between ${field.min} and ${field.max}.`;
        return;
      }
      payload[field.name] = numeric;
    }
    this.loading = true;
    this.api.predict(payload).subscribe({
      next: result => { this.result = result; this.loading = false; },
      error: err => {
        this.error = `API error ${err.status || ''}: ${err.error?.error || err.message || 'Check Flask terminal'}`;
        this.loading = false;
      },
    });
  }
}
