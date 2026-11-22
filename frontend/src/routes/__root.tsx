import {
  createRootRoute,
  Outlet,
} from "@tanstack/react-router";
import {Button} from "@/components/ui/button";

export const Route = createRootRoute({
  component: () => <Outlet />,
  notFoundComponent: NotFound,
});



export default function NotFound() {
    return (
        <div>
            <h1>404</h1>
            <p>Sorry, this page does not exist.</p>
            <Button variant="secondary" onClick={() => window.location.href = "/"}>
                Go Home
            </Button>
        </div>
    );
}