import { useForm } from "react-hook-form";
import useAuthContext from "@App/lib/auth/AuthContext";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import RegistrationGuard from "@App/lib/user/RegistrationGuard";
import Button from "@App/components/atoms/Button";
import { Select } from "@App/components/Select";
import UserService from "@App/lib/user/UserService";
import styles from "@App/styles/RegisterPage.module.scss";
import StorageService, {
  EStorageFolders,
} from "@App/lib/storage/StorageService";
import {
  IBaseUserAttributes,
  EUserConcentrations,
  EUserProficiencies,
} from "@App/lib/user/models";
import { TextField } from "@App/components/molecules/TextField";

interface RegFormInputs extends IBaseUserAttributes {
  avatar: FileList;
}

const inputValidationSchema = yup
  .object({
    name: yup.string().max(255).required("Name is required"),
    concentration: yup.string().max(255).required("Concentration is required"),
    proficiency: yup.string().max(255).required("Proficiency is required"),
  })
  .required();

export default function RegisterPage() {
  const { currentUser, fetchUser } = useAuthContext();
  const {
    register,
    handleSubmit,
    formState: { errors: formError },
  } = useForm<RegFormInputs>({
    mode: "onSubmit",
    resolver: yupResolver(inputValidationSchema),
  });

  const onSubmit = async (data: RegFormInputs) => {
    const { name, concentration, proficiency } = data;

    const avatarUrl = await StorageService.upload(
      data.avatar[0],
      EStorageFolders.profilePic,
      currentUser!.id
    );

    UserService.registerUser(currentUser!.id, {
      name,
      concentration,
      proficiency,
      avatarUrl,
    });
    await fetchUser();
  };

  return (
    <RegistrationGuard>
      <div className={styles.registerBox}>
        <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
          <h1>Register</h1>
          <label>Select a profile picture:</label>
          <input type="file" required accept="image/*" {...register("avatar")} />
          <label>Enter your name:</label>
          <TextField placeholder="Full Name" {...register("name")} />
          {formError.name && <span>{formError.name.message}</span>}

          <label>Select a concentration:</label>
          <Select {...register("concentration")}>
            {Object.values(EUserConcentrations).map((concentration) => (
              <option value={concentration} key={concentration}>
                {concentration}
              </option>
            ))}
          </Select>
          {formError.concentration && (
            <span>{formError.concentration.message}</span>
          )}

          <label>Select a proficiency:</label>
          <select {...register("proficiency")}>
            {Object.values(EUserProficiencies).map((proficiency) => (
              <option value={proficiency} key={proficiency}>
                {proficiency}
              </option>
            ))}
          </select>
          {formError.proficiency && (
            <span>{formError.proficiency.message}</span>
          )}

          <Button type="submit">sign up</Button>
        </form>
      </div>
    </RegistrationGuard>
  );
}
