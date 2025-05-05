import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';
import '@testing-library/jest-dom'; // for the 'toBeInTheDocument' matcher

// Mock the fetch API call
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve([]), // return an empty array for testing
  })
);

test('renders search input fields and button', () => {
  render(<App />);

  // Check if the input fields and button are present
  expect(screen.getByPlaceholderText('Search item...')).toBeInTheDocument();
  expect(screen.getByPlaceholderText('Min price')).toBeInTheDocument();
  expect(screen.getByPlaceholderText('Max price')).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /search/i })).toBeInTheDocument();
});

test('displays loading indicator when searching', async () => {
  render(<App />);

  fireEvent.change(screen.getByPlaceholderText('Search item...'), {
    target: { value: 'iphone' },
  });
  fireEvent.change(screen.getByPlaceholderText('Min price'), {
    target: { value: '100' },
  });
  fireEvent.change(screen.getByPlaceholderText('Max price'), {
    target: { value: '500' },
  });

  fireEvent.click(screen.getByRole('button', { name: /search/i }));

  // Check if the loading indicator is shown
  expect(screen.getByText('Loading...')).toBeInTheDocument();

  // Simulate a delay
  await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));
});

test('displays error when fields are empty and search is triggered', () => {
  render(<App />);

  fireEvent.click(screen.getByRole('button', { name: /search/i }));

  // Check if the alert is triggered when fields are empty
  expect(window.alert).toHaveBeenCalledWith('Please fill in all fields before searching!');
});
