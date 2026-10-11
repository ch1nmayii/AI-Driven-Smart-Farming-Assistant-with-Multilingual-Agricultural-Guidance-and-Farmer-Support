import { AdminDashboard } from '@/components/AdminDashboard';

export const metadata = {
  title: 'Agricultural Extension Worker Portal | Kisan AI',
  description: 'Admin dashboard for chatbot monitoring, flagged query review, and knowledge base curation',
};

export default function AdminPage() {
  return <AdminDashboard />;
}
