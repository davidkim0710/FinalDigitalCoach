import React from 'react';
import AuthGuard from "@App/lib/auth/AuthGuard";
import ForumApp from '@App/components/organisms/Forum/ForumApp';

export default function ConnectionsPage() {
  return (
    <AuthGuard>
      <div>
        <h1>Connections Page</h1>
        <ForumApp />
      </div>
    </AuthGuard>
  );
}
