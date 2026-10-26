import { provideHttpClient } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('App', () => {
  it('shows the model task and all training inputs', async () => {
    await TestBed.configureTestingModule({ imports: [App], providers: [provideHttpClient()] }).compileComponents();
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Football position classifier');
    expect(fixture.componentInstance.fields.length).toBe(41);
  });
});
