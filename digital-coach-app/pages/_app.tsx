import type { AppProps } from "next/app";
import { useEffect } from 'react';
import { seed } from './path/to/seedFile'; // Adjust the path to your seed file as needed

import "@App/styles/globals.css";
import "@fullcalendar/common/main.css";
import "@fullcalendar/daygrid/main.css";
import "@App/lib/firebase/firebase.config";
import CoreLayout from "@App/components/layouts/CoreLayout";
import { AuthContextProvider } from "@App/lib/auth/AuthContextProvider";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "react-query/devtools";

async function MyApp({ Component, pageProps }: AppProps) {
  const queryClient = new QueryClient();

  useEffect(() => {
    // Call the seed function when the app starts
    async function seedData() {
      await seed();
    }
    seedData();
  }, []); // Ensure the seed function is called only once, when the component mounts

  return (
    <QueryClientProvider client={queryClient}>
      <AuthContextProvider>
        <CoreLayout>
          <Component {...pageProps} />
        </CoreLayout>
      </AuthContextProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export default MyApp;
