// src/pages/page.tsx
import Link from 'next/link';

export default function Home() {
  return (
    <>
      <Link href="/email-verification">Verify Email</Link><br/>
      <Link href="/push-notification">Click for Notificaton</Link><br />
      <Link href="/push-noti"> Messages Notification 2</Link><br />
      <Link href="/product_announcement">Product Announcement</Link><br />
      <Link href="/special_offers">Special Offers</Link><br />
      <Link href="/insights_tips">Insights Tips</Link><br />
      <Link href="/price_alerts">Price Alerts</Link><br />
      <Link href="/account_activity">Account Activity</Link><br />
    </>
  );
}
