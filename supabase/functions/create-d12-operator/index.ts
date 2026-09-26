import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { withSupabase } from "npm:@supabase/server@^1";

export default {
  fetch: withSupabase(
    { auth: "none" },
    async (req, ctx) => {
      try {
        if (req.method !== "POST") {
          return Response.json(
            {
              success: false,
              error: "Only POST requests are allowed."
            },
            { status: 405 }
          );
        }

        // --------------------------------------------------
        // 1. Get the user's access token
        // --------------------------------------------------

        const authHeader = req.headers.get("Authorization");

        if (!authHeader || !authHeader.startsWith("Bearer ")) {
          return Response.json(
            {
              success: false,
              error: "Missing authentication token."
            },
            { status: 401 }
          );
        }

        const token = authHeader.substring(7).trim();

        if (!token) {
          return Response.json(
            {
              success: false,
              error: "Invalid authentication token."
            },
            { status: 401 }
          );
        }

        console.log("D12 operator creation request received.");

        // --------------------------------------------------
        // 2. Verify the signed-in user
        // --------------------------------------------------

        const {
          data: { user },
          error: userError
        } = await ctx.supabaseAdmin.auth.getUser(token);

        if (userError || !user) {
          console.error(
            "Authentication verification failed:",
            userError?.message
          );

          return Response.json(
            {
              success: false,
              error: "Your login session is invalid or has expired."
            },
            { status: 401 }
          );
        }

        console.log("Authenticated user:", user.id);

        // --------------------------------------------------
        // 3. Verify administrator profile
        // --------------------------------------------------

        const {
          data: adminProfile,
          error: profileError
        } = await ctx.supabaseAdmin
          .from("profiles")
          .select("id, full_name, role")
          .eq("id", user.id)
          .maybeSingle();

        if (profileError) {
          console.error(
            "Admin profile lookup failed:",
            profileError.message
          );

          return Response.json(
            {
              success: false,
              error:
                "Unable to verify administrator permissions: " +
                profileError.message
            },
            { status: 500 }
          );
        }

        if (!adminProfile) {
          return Response.json(
            {
              success: false,
              error:
                "No D12 profile exists for the signed-in administrator."
            },
            { status: 403 }
          );
        }

        if (adminProfile.role !== "admin") {
          return Response.json(
            {
              success: false,
              error:
                "Access denied. Only a D12 administrator can create operators."
            },
            { status: 403 }
          );
        }

        console.log(
          "Administrator verified:",
          adminProfile.full_name
        );

        // --------------------------------------------------
        // 4. Read operator information
        // --------------------------------------------------

        const body = await req.json();

        const full_name =
          typeof body.full_name === "string"
            ? body.full_name.trim().replace(/\s+/g, " ")
            : "";

        const email =
          typeof body.email === "string"
            ? body.email.trim().toLowerCase()
            : "";

        const password =
          typeof body.password === "string"
            ? body.password
            : "";

        const whatsapp_number = typeof body.whatsapp_number === "string" ? body.whatsapp_number.trim() : "";
        if (whatsapp_number && !/^[1-9]\d{7,14}$/.test(whatsapp_number)) return Response.json({success:false,error:"Enter a valid WhatsApp number with country code."},{status:400});
        if (!full_name || full_name.length > 60) {
          return Response.json(
            {
              success: false,
              error: "Operator full name is required."
            },
            { status: 400 }
          );
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) {
          return Response.json(
            {
              success: false,
              error: "Operator email is required."
            },
            { status: 400 }
          );
        }

        if (!password || password.length < 6) {
          return Response.json(
            {
              success: false,
              error:
                "Operator password must be at least 6 characters."
            },
            { status: 400 }
          );
        }

        // --------------------------------------------------
        // 5. Create Supabase Auth user
        // --------------------------------------------------

        console.log("Creating operator Auth account:", email);

        const {
          data: authResult,
          error: authError
        } = await ctx.supabaseAdmin.auth.admin.createUser({
          email,
          password,
          email_confirm: true,
          user_metadata: {
            whatsapp_number,
            full_name
          }
        });

        if (authError) {
          console.error(
            "Auth user creation failed:",
            authError.message
          );

          return Response.json(
            {
              success: false,
              error: authError.message
            },
            { status: 400 }
          );
        }

        if (!authResult?.user) {
          return Response.json(
            {
              success: false,
              error:
                "Supabase did not return the newly created user."
            },
            { status: 500 }
          );
        }

        const newUser = authResult.user;

        console.log(
          "Auth user created:",
          newUser.id
        );

        // --------------------------------------------------
        // 6. Create D12 operator profile
        // --------------------------------------------------

        const {
          error: operatorProfileError
        } = await ctx.supabaseAdmin
          .from("profiles")
          .upsert(
            {
              id: newUser.id,
              full_name,
              role: "operator"
            },
            {
              onConflict: "id"
            }
          );

        if (operatorProfileError) {
          console.error(
            "Operator profile creation failed:",
            operatorProfileError.message
          );

          // Roll back the Auth account
          try {
            await ctx.supabaseAdmin.auth.admin.deleteUser(
              newUser.id
            );
          } catch (rollbackError) {
            console.error(
              "Rollback failed:",
              rollbackError
            );
          }

          return Response.json(
            {
              success: false,
              error:
                "The Auth account was created but the D12 operator profile failed: " +
                operatorProfileError.message
            },
            { status: 500 }
          );
        }

        // --------------------------------------------------
        // 7. Success
        // --------------------------------------------------

        console.log(
          "D12 operator created successfully:",
          email
        );

        return Response.json({
          success: true,
          message: "D12 operator created successfully.",
          operator: {
            id: newUser.id,
            full_name,
            email,
            role: "operator"
          }
        });

      } catch (error) {
        console.error(
          "Unexpected D12 operator creation error:",
          error
        );

        return Response.json(
          {
            success: false,
            error:
              error instanceof Error
                ? error.message
                : "An unexpected error occurred."
          },
          { status: 500 }
        );
      }
    }
  )
};
