import "globals.css";
import { TopNavBar } from "components/TopNavBar";
import { Analytics } from "@vercel/analytics/react";
import { AuthProvider } from "./context/AuthContext";
import { ResumeProvider } from "./context/ResumeContext";

export const metadata = {
  title: "NLP Resume Builder",
  description: ""
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full overflow-x-hidden">
      <AuthProvider>
      <ResumeProvider>
      <body className="h-full m-0 p-0 overflow-x-hidden">
        <div className="flex flex-col min-h-screen">
          <TopNavBar />
          <main className="flex-grow">
            {children}
          </main>
        </div>
        <Analytics />
      </body>
      </ResumeProvider>
      </AuthProvider>
    </html>
  );
}