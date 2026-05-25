// Root page redirects to the chat interface
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/chat");
}
