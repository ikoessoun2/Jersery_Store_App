/* src/components/Layouts/MainLayout.tsx */
import Sidebar from "./Sidebar";
import {Outlet} from "@tanstack/react-router";
import { useIsMobile } from "../../hooks/useIsMobile";


export default function MainLayout() {
  const isMobile = useIsMobile();
  const menuItems = [
    { label: "Home", link: "/" },
    { label: "Catalog", link: "/catalog" },
    { label: "About", link: "/about" },
  ];

  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <Sidebar menuItems={menuItems} isMobile={isMobile}/>

      {/* Main Content */}
      <main className="relative p-4 flex-1 bg-slate-100">
        <Outlet/>
      </main>

    </div>
  );
}