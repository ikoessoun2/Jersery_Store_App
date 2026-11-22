import { createFileRoute } from "@tanstack/react-router";
import MainLayout from "../../components/Layouts/MainLayout";

export const Route = createFileRoute("/_main")({
  component: () => (
    <MainLayout />
  ),
});