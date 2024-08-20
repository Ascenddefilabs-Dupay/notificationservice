// src/pages/page.tsx
import Link from 'next/link';

export default function Home() {
  return (
    <>
      <Link href="/email-verification">Verify Email</Link><br/>
      <Link href="/push-notification">Click for Notificaton</Link><br />
      <Link href="/push-noti">Notification 2</Link><br />
      <Link href="/product_announcement">Product Announcement</Link>
    </>
  );
}
