import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { withSupabase } from "npm:@supabase/server@^1";

export default {
  fetch: withSupabase(
    { auth: "none" },
    async (req, ctx) => {
      try {
        if (req.method !== "POST") {
          return Response.json({ success: false, error: "Only POST requests are allowed." }, { status: 405 });
        }

        const authHeader = req.headers.get("Authorization");
        if (!authHeader || !authHeader.startsWith("Bearer ")) {
          return Response.json({ success: false, error: "Missing authentication token." }, { status: 401 });
        }

        const token = authHeader.substring(7).trim();
        const { data: { user }, error: userError } = await ctx.supabaseAdmin.auth.getUser(token);
        if (userError || !user) {
          return Response.json({ success: false, error: "Your login session is invalid or has expired." }, { status: 401 });
        }

        const { data: adminProfile, error: profileError } = await ctx.supabaseAdmin
          .from("profiles")
          .select("id, full_name, role")
          .eq("id", user.id)
          .maybeSingle();

        if (profileError) {
          return Response.json({ success: false, error: "Unable to verify administrator permissions: " + profileError.message }, { status: 500 });
        }
        if (!adminProfile || adminProfile.role !== "admin") {
          return Response.json({ success: false, error: "Access denied. Only a D12 administrator can delete operators." }, { status: 403 });
        }

        const body = await req.json();
        const operatorId = typeof body.operator_id === "string" ? body.operator_id.trim() : "";
        if (!operatorId) {
          return Response.json({ success: false, error: "Operator ID is required." }, { status: 400 });
        }
        if (operatorId === user.id) {
          return Response.json({ success: false, error: "The administrator account cannot be deleted from this control." }, { status: 400 });
        }

        const { data: operatorProfile, error: operatorError } = await ctx.supabaseAdmin
          .from("profiles")
          .select("id, full_name, role")
          .eq("id", operatorId)
          .maybeSingle();

        if (operatorError) {
          return Response.json({ success: false, error: operatorError.message }, { status: 500 });
        }
        if (!operatorProfile || operatorProfile.role !== "operator") {
          return Response.json({ success: false, error: "The selected account is not a D12 operator." }, { status: 404 });
        }

        const {data: assignments,error: assignmentError}=await ctx.supabaseAdmin.from("table_assignments").select("table_id").eq("operator_id",operatorId).eq("active",true);
        if(assignmentError)throw assignmentError;
        // Auth deletion cascades atomically to profiles and assignments; match history uses SET NULL.
        const {error: authDeleteError}=await ctx.supabaseAdmin.auth.admin.deleteUser(operatorId);
        if(authDeleteError)return Response.json({success:false,error:"Unable to delete operator: "+authDeleteError.message},{status:500});
        let warning="";
        for(const tableId of new Set((assignments||[]).map(a=>a.table_id))){
          const {count,error}=await ctx.supabaseAdmin.from("table_assignments").select("id",{head:true,count:"exact"}).eq("table_id",tableId).eq("active",true);
          if(error){warning="Refresh table status before reassigning.";continue;}
          if(count===0){const result=await ctx.supabaseAdmin.from("cue_tables").update({status:"available"}).eq("id",tableId);if(result.error)warning="Refresh table status before reassigning.";}
        }

        return Response.json({
          success: true,
          warning,
          message: "D12 operator deleted successfully.",
          operator: { id: operatorId, full_name: operatorProfile.full_name, role: "operator" }
        });
      } catch (error) {
        console.error("D12 delete operator error:", error);
        return Response.json({ success: false, error: error instanceof Error ? error.message : "An unexpected error occurred." }, { status: 500 });
      }
    }
  )
};

