import AuthGuard from "@App/lib/auth/AuthGuard";

export default function ConnectionsPage() {
  return (
    <AuthGuard>
      <h1>Connections Page</h1>
    </AuthGuard>
  );
}
